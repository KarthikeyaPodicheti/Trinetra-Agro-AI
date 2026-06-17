import { apiClient, setCookie, deleteCookie } from "./api";
import type { TokenResponse, UserResponse } from "./types";

export async function login(email: string, password: string): Promise<boolean> {
  try {
    const data = await apiClient.post<TokenResponse>("/auth/login", { email, password });
    setCookie("access_token", data.access_token, 1);
    setCookie("refresh_token", data.refresh_token, 7);
    return true;
  } catch {
    return false;
  }
}

export async function register(
  email: string,
  password: string,
  fullName?: string,
  phone?: string
): Promise<boolean> {
  try {
    await apiClient.post<TokenResponse>("/auth/register", {
      email,
      password,
      full_name: fullName || undefined,
      phone: phone || undefined,
    });
    return login(email, password);
  } catch {
    return false;
  }
}

// ── OTP Auth ────────────────────────────────────────────────────────────

export async function sendOtp(phone: string): Promise<string | null> {
  try {
    const data: Record<string, unknown> = await apiClient.post("/auth/send-otp", { phone });
    // In console mode the OTP is returned directly for testing
    return typeof data.otp === "string" ? data.otp : null;
  } catch {
    return null;
  }
}

export async function verifyOtp(phone: string, otp: string): Promise<boolean> {
  try {
    const data = await apiClient.post<TokenResponse>("/auth/verify-otp", { phone, otp });
    setCookie("access_token", data.access_token, 1);
    setCookie("refresh_token", data.refresh_token, 7);
    return true;
  } catch {
    return false;
  }
}

// ── Session ────────────────────────────────────────────────────────────

export function logout() {
  deleteCookie("access_token");
  deleteCookie("refresh_token");
}

export async function getUser(): Promise<UserResponse | null> {
  try {
    return await apiClient.get<UserResponse>("/auth/me");
  } catch {
    return null;
  }
}
