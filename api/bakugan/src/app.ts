import { Hono } from "hono";
import { logger } from "hono/logger";

const app = new Hono().basePath("/api/bakugan");

app.use(logger());

app.get("/", (c) => {
  return c.json({ message: "Hello World!" });
});

app.get("/status", (c) => {
  return c.json({ status: "!ok" });
});

export default app;
