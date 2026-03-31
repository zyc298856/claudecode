import { getAllPosts } from "@/lib/posts";
import type { MetadataRoute } from "next";

const BASE_URL = "https://your-domain.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const posts = getAllPosts();
  const postUrls = posts.map((post) => ({
    url: `${BASE_URL}/posts/${post.slug}`,
    lastModified: new Date(post.date),
  }));

  return [
    { url: BASE_URL, lastModified: new Date() },
    { url: `${BASE_URL}/posts`, lastModified: new Date() },
    { url: `${BASE_URL}/categories`, lastModified: new Date() },
    { url: `${BASE_URL}/tags`, lastModified: new Date() },
    { url: `${BASE_URL}/search`, lastModified: new Date() },
    { url: `${BASE_URL}/about`, lastModified: new Date() },
    ...postUrls,
  ];
}
