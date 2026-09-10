import { z } from "zod";

export const createTodoSchema = z.object({
  title: z
    .string()
    .min(1, "title は必須です")
    .max(120, "title は120文字以内で入力してください"),
});

export const updateTodoSchema = z.object({
  title: z
    .string()
    .min(1, "title は空にできません")
    .max(120, "title は120文字以内で入力してください")
    .optional(),
  completed: z.boolean().optional(),
});

export type CreateTodoInput = z.infer<typeof createTodoSchema>;
export type UpdateTodoInput = z.infer<typeof updateTodoSchema>;
