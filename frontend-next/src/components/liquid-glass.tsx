import React from "react";

interface LiquidGlassProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "card" | "button" | "panel" | "dock";
  strong?: boolean;
  as?: React.ElementType;
  children?: React.ReactNode;
}

/**
 * LiquidGlass — wraps content in the macOS liquid-glass layered effect.
 * Renders 4 stacked layers: distortion+blur, tint, shine, content.
 * Requires <GlassFilter /> mounted somewhere globally.
 */
export function LiquidGlass({
  variant = "card",
  strong = false,
  as = "div",
  className = "",
  children,
  style,
  ...rest
}: LiquidGlassProps) {
  const Tag = as as any;
  return (
    <Tag
      className={`liquidGlass-wrapper liquidGlass-${variant} ${className}`}
      style={{ position: "relative", overflow: "hidden", ...style }}
      {...rest}
    >
      <div className="liquidGlass-effect" data-strong={strong ? "true" : undefined} />
      <div className="liquidGlass-tint" />
      <div className="liquidGlass-shine" />
      <div className="liquidGlass-content" style={{ position: "relative", zIndex: 3 }}>
        {children}
      </div>
    </Tag>
  );
}
