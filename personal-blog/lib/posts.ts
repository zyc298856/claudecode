import fs from "fs";
import path from "path";
import matter from "gray-matter";

const postsDirectory = path.join(process.cwd(), "content/posts");

export interface PostMeta {
  slug: string;
  title: string;
  date: string;
  category: string;
  tags: string[];
  description: string;
  draft: boolean;
}

export function getAllPosts(): PostMeta[] {
  const fileNames = fs.readdirSync(postsDirectory);
  const posts = fileNames
    .filter((name) => name.endsWith(".mdx"))
    .map((fileName) => {
      const slug = fileName.replace(/\.mdx$/, "");
      const fullPath = path.join(postsDirectory, fileName);
      const fileContents = fs.readFileSync(fullPath, "utf8");
      const { data } = matter(fileContents);
      return {
        slug,
        title: data.title as string,
        date: data.date as string,
        category: data.category as string,
        tags: (data.tags as string[]) || [],
        description: data.description as string,
        draft: (data.draft as boolean) || false,
      };
    })
    .filter((post) => !post.draft)
    .sort((a, b) => (a.date > b.date ? -1 : 1));
  return posts;
}

export function getPostBySlug(slug: string): { meta: PostMeta; content: string } {
  const fullPath = path.join(postsDirectory, `${slug}.mdx`);
  const fileContents = fs.readFileSync(fullPath, "utf8");
  const { data, content } = matter(fileContents);
  return {
    meta: {
      slug,
      title: data.title as string,
      date: data.date as string,
      category: data.category as string,
      tags: (data.tags as string[]) || [],
      description: data.description as string,
      draft: (data.draft as boolean) || false,
    },
    content,
  };
}

export function getAllCategories(): string[] {
  const posts = getAllPosts();
  return [...new Set(posts.map((post) => post.category))];
}

export function getAllTags(): string[] {
  const posts = getAllPosts();
  return [...new Set(posts.flatMap((post) => post.tags))];
}

export function getPostsByCategory(category: string): PostMeta[] {
  return getAllPosts().filter((post) => post.category === category);
}

export function getPostsByTag(tag: string): PostMeta[] {
  return getAllPosts().filter((post) => post.tags.includes(tag));
}
