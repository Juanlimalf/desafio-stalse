import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  console.log("Proxy request:", request.url);
  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/metrics", "/tickets"],
};
