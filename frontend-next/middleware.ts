import { NextRequest, NextResponse } from "next/server";

export const config = {
  matcher: ["/((?!_next|api|bg\.jpg|favicon\.ico|login|register).*)"],
};

interface JwtPayload {
  exp?: number;
  sub?: string;
  type?: string;
}

function decodeTokenPayload(token: string): JwtPayload | null {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
}

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const refreshToken = request.cookies.get("refresh_token")?.value;

  if (!token && !refreshToken) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // If access token is missing/expired but refresh token exists, allow through
  // The client-side api.ts will handle the token refresh automatically
  if (!token || !decodeTokenPayload(token)?.exp) {
    if (refreshToken) return NextResponse.next();
    return NextResponse.redirect(new URL("/login", request.url));
  }

  const payload = decodeTokenPayload(token);
  if (payload && payload.exp && payload.exp * 1000 < Date.now()) {
    if (refreshToken) return NextResponse.next();
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}
