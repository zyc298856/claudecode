"use client";

import { useState, useCallback, useMemo } from "react";
import Fuse, { type FuseResult } from "fuse.js";
import type { SearchEntry } from "@/lib/search";
import Link from "next/link";

interface SearchBarProps {
  entries: SearchEntry[];
}

export function SearchBar({ entries }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<FuseResult<SearchEntry>[]>([]);

  const fuse = useMemo(
    () =>
      new Fuse(entries, {
        keys: ["title", "description", "tags", "category", "content"],
        threshold: 0.3,
      }),
    [entries]
  );

  const handleSearch = useCallback(
    (value: string) => {
      setQuery(value);
      if (value.trim()) {
        setResults(fuse.search(value));
      } else {
        setResults([]);
      }
    },
    [fuse]
  );

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
        placeholder="搜索文章..."
        className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400 text-lg"
        autoFocus
      />
      {results.length > 0 && (
        <div className="mt-6 space-y-4">
          {results.map(({ item }) => (
            <Link
              key={item.slug}
              href={`/posts/${item.slug}`}
              className="block p-4 rounded-lg border border-gray-100 hover:border-blue-300 transition-colors"
            >
              <h3 className="font-semibold">{item.title}</h3>
              <p className="text-sm text-gray-500 mt-1">{item.description}</p>
              <div className="mt-2 text-xs text-gray-400">
                {item.category} &middot; {item.tags.join(", ")}
              </div>
            </Link>
          ))}
        </div>
      )}
      {query && results.length === 0 && (
        <p className="mt-6 text-gray-400 text-center">没有找到相关文章</p>
      )}
    </div>
  );
}
