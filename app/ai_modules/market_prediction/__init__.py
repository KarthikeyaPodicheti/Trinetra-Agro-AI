"""
Trinetra Agro AI - Market Price Prediction Module
Statistical time-series forecasting (MA + trend + seasonality).
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from utils.data_sources import fetch_mandi_prices


class MarketPredictor:
    """
    Market Price Prediction using statistical methods.
    No heavy ML libraries required.
    """

    BASE_PRICES = {
        'rice':      {'price': 2200,  'volatility': 'low',    'trend': 'stable'},
        'wheat':     {'price': 2150,  'volatility': 'low',    'trend': 'rising'},
        'cotton':    {'price': 5500,  'volatility': 'high',   'trend': 'rising'},
        'sugarcane': {'price': 350,   'volatility': 'low',    'trend': 'stable'},
        'tomato':    {'price': 1800,  'volatility': 'high',   'trend': 'volatile'},
        'potato':    {'price': 1200,  'volatility': 'medium', 'trend': 'stable'},
        'onion':     {'price': 1500,  'volatility': 'high',   'trend': 'volatile'},
        'maize':     {'price': 1900,  'volatility': 'medium', 'trend': 'stable'},
        'soybean':   {'price': 4500,  'volatility': 'medium', 'trend': 'rising'},
        'mustard':   {'price': 5200,  'volatility': 'medium', 'trend': 'stable'},
        'groundnut': {'price': 5000,  'volatility': 'medium', 'trend': 'stable'},
    }

    SEASONALITY = {
        1: 0.90, 2: 0.85, 3: 0.95, 4: 1.00, 5: 1.10, 6: 1.15,
        7: 1.20, 8: 1.25, 9: 1.10, 10: 1.00, 11: 0.95, 12: 0.90,
    }

    def __init__(self):
        self.historical_data = {}
        self._generate_all()

    def _generate_all(self):
        for crop in self.BASE_PRICES:
            self.historical_data[crop] = self._generate_history(crop)

    def _generate_history(self, crop, days=365):
        info = self.BASE_PRICES[crop]
        base = info['price']
        end = datetime.now()
        dates = pd.date_range(end=end, periods=days, freq='D')
        rng = np.random.default_rng(hash(crop) % 2**31)

        vol_map = {'high': 0.12, 'medium': 0.06, 'low': 0.03}
        sigma = base * vol_map.get(info['volatility'], 0.06)

        prices = []
        for i, d in enumerate(dates):
            p = base * self.SEASONALITY.get(d.month, 1.0)
            if info['trend'] == 'rising':
                p *= (1 + 0.0008 * i)
            p += rng.normal(0, sigma)
            prices.append(max(p, base * 0.4))

        return pd.DataFrame({'date': dates, 'price': prices})

    # ------------------------------------------------------------------
    def predict_prices(self, crop: str, days: int = 30, location: str = None) -> dict:
        crop = crop.lower().strip()
        if crop not in self.BASE_PRICES:
            return {'success': False,
                    'error': f'Crop "{crop}" not supported. Available: {list(self.BASE_PRICES)}'}

        df = self.historical_data[crop]
        current_price = float(df['price'].iloc[-1])
        source_info = {
            'current_price_source': 'synthetic-history',
            'current_price_updated_at': datetime.now().isoformat(),
            'market_records_used': 0,
        }

        market_live = fetch_mandi_prices(crop=crop, location=location)
        if market_live.get('success'):
            current_price = float(market_live['current_price'])
            source_info = {
                'current_price_source': market_live.get('source', 'data.gov.in'),
                'current_price_updated_at': market_live.get('updated_at'),
                'market_records_used': int(market_live.get('records_used', 0)),
                'markets': market_live.get('markets', []),
                'states': market_live.get('states', []),
            }
        else:
            source_info['source_error'] = market_live.get('error', 'market API unavailable')

        # Three forecast methods
        ma_pred = self._moving_avg_predict(df, days)
        trend_pred = self._trend_predict(df, days)
        seasonal_pred = self._seasonal_predict(df, days)
        ensemble = (ma_pred + trend_pred + seasonal_pred) / 3

        trend = self._calc_trend(ensemble)
        rec = self._recommend(ensemble, trend)
        conf = self._confidence(ma_pred, trend_pred, seasonal_pred, ensemble)

        pred_dates = [(datetime.now() + timedelta(days=i + 1)).strftime('%Y-%m-%d')
                      for i in range(days)]

        return {
            'success': True,
            'crop': crop,
            'current_price': round(current_price, 2),
            'currency': '₹/quintal',
            'days_predicted': days,
            'predictions': {
                'dates': pred_dates,
                'prices': [round(p, 2) for p in ensemble],
                'moving_avg': [round(p, 2) for p in ma_pred],
                'trend': [round(p, 2) for p in trend_pred],
                'seasonal': [round(p, 2) for p in seasonal_pred],
            },
            'trend': trend,
            'recommendation': rec,
            'confidence': conf,
            'volatility': self.BASE_PRICES[crop]['volatility'],
            'market_tips': self._tips(crop, trend),
            'data_source': source_info,
        }

    # --- forecasters ---
    def _moving_avg_predict(self, df, days):
        ma7 = df['price'].tail(7).mean()
        ma30 = df['price'].tail(30).mean()
        base = 0.6 * ma7 + 0.4 * ma30
        return np.full(days, base)

    def _trend_predict(self, df, days):
        recent = df['price'].tail(60).values
        x = np.arange(len(recent))
        coeffs = np.polyfit(x, recent, 1)
        slope, intercept = coeffs
        future_x = np.arange(len(recent), len(recent) + days)
        return np.polyval(coeffs, future_x)

    def _seasonal_predict(self, df, days):
        base = df['price'].tail(30).mean()
        now = datetime.now()
        preds = []
        for i in range(days):
            d = now + timedelta(days=i + 1)
            mult = self.SEASONALITY.get(d.month, 1.0)
            preds.append(base * mult)
        return np.array(preds)

    # --- helpers ---
    def _calc_trend(self, preds):
        if len(preds) < 7:
            return 'stable'
        first = np.mean(preds[:7])
        last = np.mean(preds[-7:]) if len(preds) >= 14 else np.mean(preds[-3:])
        pct = (last - first) / first * 100
        if pct > 5:
            return 'rising'
        elif pct < -5:
            return 'falling'
        return 'stable'

    def _confidence(self, a, b, c, ens):
        std = np.std(np.array([a, b, c]), axis=0)
        cv = np.mean(std) / np.mean(ens) if np.mean(ens) else 1
        if cv < 0.05:
            return 'High'
        elif cv < 0.10:
            return 'Medium'
        return 'Low'

    def _recommend(self, preds, trend):
        cur = preds[0]
        w1 = np.mean(preds[:7])
        pct = (w1 - cur) / cur * 100 if cur else 0
        if trend == 'rising':
            return {'action': 'WAIT', 'message': f'Prices expected to rise ~{abs(pct):.1f}% this week',
                    'reason': 'Hold produce for better prices', 'urgency': 'medium'}
        elif trend == 'falling':
            return {'action': 'SELL NOW', 'message': f'Prices may drop ~{abs(pct):.1f}% this week',
                    'reason': 'Sell now to maximise returns', 'urgency': 'high'}
        return {'action': 'HOLD', 'message': 'Prices expected to stay stable (±5%)',
                'reason': 'No major change expected', 'urgency': 'low'}

    def _tips(self, crop, trend):
        tips = []
        seasonal_tips = {
            'rice': 'Rice prices often peak during lean supply months (Apr-Jun)',
            'wheat': 'Wheat prices historically higher before Rabi harvest',
            'cotton': 'Monitor international cotton prices — they drive local rates',
            'tomato': 'Tomato prices are highly seasonal — time your harvest well',
            'onion': 'Onion prices can spike dramatically — proper storage helps',
        }
        if crop in seasonal_tips:
            tips.append(seasonal_tips[crop])
        if trend == 'rising':
            tips.append('Consider storing produce if you have cold-storage access')
        elif trend == 'falling':
            tips.append('Sell quickly or explore processing / value-addition')
        tips.append('Check your nearest mandi prices on eNAM (enam.gov.in)')
        return tips

    def get_market_overview(self):
        overview = {}
        for crop in self.BASE_PRICES:
            df = self.historical_data[crop]
            cur = float(df['price'].iloc[-1])
            w_avg = float(df['price'].tail(7).mean())
            prev_w = float(df['price'].iloc[-14:-7].mean())
            chg = (w_avg - prev_w) / prev_w * 100 if prev_w else 0
            overview[crop] = {
                'current_price': round(cur, 2),
                'week_change': round(chg, 2),
                'trend': self.BASE_PRICES[crop]['trend'],
                'volatility': self.BASE_PRICES[crop]['volatility'],
            }
        return overview


def create_market_predictor() -> MarketPredictor:
    return MarketPredictor()
    print(f"Recommendation: {result['recommendation']['action']}")
