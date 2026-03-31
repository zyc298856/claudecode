import { getAllPosts } from "@/lib/posts";

const BASE_URL = "https://your-domain.com";

export async function GET() {
  const posts = getAllPosts();
  const items = posts
    .map(
      (post) => `
    <item>
      <title>${post.title}</title>
      <link>${BASE_URL}/posts/${post.slug}</link>
      <description>${post.description}</description>
      <pubDate>${new Date(post.date).toUTCString()}</pubDate>
      <category>${post.category}</category>
    </item>`
    )
    .join("");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>My Tech Blog</title>
    <link>${BASE_URL}</link>
    <description>A personal tech blog</description>
    <language>zh-CN</language>
    ${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: { "Content-Type": "application/xml" },
  });
}
