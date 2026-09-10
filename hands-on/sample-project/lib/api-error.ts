import { NextResponse } from "next/server";
import type { ZodError } from "zod";

export type ApiErrorBody = {
  error: {
    code: string;
    message: string;
    details?: Record<string, string[]>;
  };
};

function errorResponse(status: number, code: string, message: string, details?: Record<string, string[]>) {
  const body: ApiErrorBody = { error: { code, message } };
  if (details) {
    body.error.details = details;
  }
  return NextResponse.json(body, { status });
}

export function badRequest(message: string) {
  return errorResponse(400, "BAD_REQUEST", message);
}

export function notFound(message: string) {
  return errorResponse(404, "NOT_FOUND", message);
}

/** zod の検証エラーを 400 レスポンスに変換する */
export function validationError(error: ZodError) {
  const message = error.errors.map((issue) => issue.message).join(", ");
  const details = error.flatten().fieldErrors as Record<string, string[]>;
  return errorResponse(400, "VALIDATION_ERROR", message, details);
}
