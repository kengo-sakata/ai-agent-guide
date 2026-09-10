import { NextResponse } from "next/server";
import { badRequest, validationError } from "@/lib/api-error";
import { createTodoSchema } from "@/lib/schema";
import { createTodo, listTodos } from "@/lib/store";

export async function GET() {
  return NextResponse.json({ todos: listTodos() });
}

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return badRequest("リクエストボディをJSONとして解釈できません");
  }

  const parsed = createTodoSchema.safeParse(body);
  if (!parsed.success) {
    return validationError(parsed.error);
  }

  const todo = createTodo(parsed.data);
  return NextResponse.json({ todo }, { status: 201 });
}
