import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import http from "node:http";
import path from "node:path";

const port = Number(process.env.PORT || 4173);
const distDir = path.resolve(process.cwd(), "dist");
const mimeTypes = new Map([
  [".css", "text/css; charset=utf-8"],
  [".html", "text/html; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".txt", "text/plain; charset=utf-8"],
  [".xml", "application/xml; charset=utf-8"]
]);

function resolveRequestPath(requestUrl) {
  const pathname = decodeURIComponent(new URL(requestUrl, "http://127.0.0.1").pathname);
  let relative = pathname.replace(/^\/+/, "");
  if (!relative) relative = "index.html";
  if (relative.endsWith("/")) relative += "index.html";
  const absolute = path.resolve(distDir, relative);
  if (absolute !== distDir && !absolute.startsWith(`${distDir}${path.sep}`)) return null;
  return absolute;
}

async function sendFile(response, filePath, statusCode = 200) {
  const info = await stat(filePath);
  if (!info.isFile()) throw new Error("not a file");
  response.writeHead(statusCode, {
    "Content-Type": mimeTypes.get(path.extname(filePath)) || "application/octet-stream",
    "Cache-Control": "no-store"
  });
  createReadStream(filePath).pipe(response);
}

const server = http.createServer(async (request, response) => {
  if (!request.url || !["GET", "HEAD"].includes(request.method || "GET")) {
    response.writeHead(405).end();
    return;
  }

  const target = resolveRequestPath(request.url);
  if (!target) {
    response.writeHead(400).end("Bad Request");
    return;
  }

  try {
    await sendFile(response, target);
  } catch {
    try {
      await sendFile(response, path.join(distDir, "404.html"), 404);
    } catch {
      response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" }).end("Not Found");
    }
  }
});

server.listen(port, "127.0.0.1", () => {
  console.log(`Serving dist at http://127.0.0.1:${port}`);
});
