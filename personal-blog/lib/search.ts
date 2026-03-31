import { getAllPosts } from "./posts";
import fs from "fs";
import path from "path";

export interface SearchEntry {
  slug: string;
  title: string;
  description: string;
  category: string;
  tags: string[];
  content: string;
}

export function buildSearchIndex(): SearchEntry[] {
  const posts = getAllPosts();
  const searchDir = path.join(process.cwd(), "content/posts");

  return posts.map((post) => {
    const fullPath = path.join(searchDir, `${post.slug}.mdx`);
    const raw = fs.readFileSync(fullPath, "utf8");
    const content = raw
      .replace(/^---[\s\S]*?---/, "")
      .replace(/#{1,6}\s/g, "")
      .replace(/\*\*/g, "")
      .replace(/`{1,3}[^`]*`{1,3}/g, "")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 500);

    return {
      slug: post.slug,
      title: post.title,
      description: post.description,
      category: post.category,
      tags: post.tags,
      content,
    };
  });
}

export function getSearchIndex(): SearchEntry[] {
  return buildSearchIndex();
}
