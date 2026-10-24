import {
  requestFormSchema,
  requestQuerySchema,
} from "@tricorder/request-ui/catalog";
import type { Stage } from "@tricorder/request-ui/model";
import { z } from "zod";

export const savedDraftSchema = z.strictObject({
  form: requestFormSchema,
  stage: requestQuerySchema.shape.stage,
});

// Capture the displayed message, including corrected company/founder names.
// Restoring it must not regenerate different words from an updated snapshot.
export const snapshotDraft = (form: unknown, stage: Stage, message: string) =>
  savedDraftSchema.parse({
    form: { ...requestFormSchema.parse(form), editedDraft: message },
    stage,
  });
