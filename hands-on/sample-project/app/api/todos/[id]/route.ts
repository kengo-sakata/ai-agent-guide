import { NextResponse } from "next/server";
import { badRequest, notFound, validationError } from "@/lib/api-error";
import { updateTodoSchema } from "@/lib/schema";
import { deleteTodo, findTodo, updateTodo } from "@/lib/store";

type RouteContext = {
  params: Promise<{ id: string }>;
};

export async function GET(_request: Request, { params }: RouteContext) {
  const { id } = await params;
  const todo = findTodo(id);
  if (!todo) {
    return notFound(`TODO(id=${id}) が見つかりません`);
  }
  return NextResponse.json({ todo });
}

export async function PATCH(request: Request, { params }: RouteContext) {
  const { id } = await params;

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return badRequest("リクエストボディをJSONとして解釈できません");
  }

  const parsed = updateTodoSchema.safeParse(body);
  if (!parsed.success) {
    return validationError(parsed.error);
  }

  const todo = updateTodo(id, parsed.data);
  if (!todo) {
    return notFound(`TODO(id=${id}) が見つかりません`);
  }
  return NextResponse.json({ todo });
}

export async function DELETE(_request: Request, { params }: RouteContext) {
  const { id } = await params;
  const deleted = deleteTodo(id);
  if (!deleted) {
    return notFound(`TODO(id=${id}) が見つかりません`);
  }
  return new NextResponse(null, { status: 204 });
}
