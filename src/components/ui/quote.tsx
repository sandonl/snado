import React from "react";

interface QuoteProps {
  children: React.ReactNode;
  author?: string;
  source?: string;
}

export function Quote({ children, author, source }: QuoteProps) {
  return (
    <blockquote className="my-6 border-l-4 border-primary pl-4 italic ">
      {children}
      {(author || source) && (
        <footer className="text-sm">
          {author && <span className="font-semibold">{author}</span>}
          {author && source && <span> — </span>}
          {source && <cite>{source}</cite>}
        </footer>
      )}
    </blockquote>
  );
}
