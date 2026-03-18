import * as z from 'zod';

export const transactionSchema = z.object({
  description: z.string().min(3, 'Description too short'),
  amount: z.string().regex(/^\d+(\.\d{1,2})?$/, 'Invalid amount'),
  account_id: z.number().positive(),
  valuta_date: z.string().datetime(),
});

export type TransactionFormValues = z.infer<typeof transactionSchema>;
