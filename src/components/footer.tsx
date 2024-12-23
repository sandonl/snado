import Link from "next/link";

export default function Footer() {
  return (
    <footer>
      <div className="px-4 py-8">
        <div className="flex flex-col items-center gap-4">
          <div className="flex gap-4">
            <Link
              href="https://linkedin.com/in/sandonlai"
              className="text-muted-foreground hover:text-primary text-xs"
              target="_blank"
              rel="noopener noreferrer"
            >
              LinkedIn
            </Link>
            <Link
              href="https://github.com/sandonl"
              className="text-muted-foreground hover:text-primary text-xs"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </Link>
            <Link
              href="https://x.com/snads_build"
              className="text-muted-foreground hover:text-primary text-xs"
              target="_blank"
              rel="noopener noreferrer"
            >
              X
            </Link>
          </div>
          <div className="text-center text-muted-foreground text-sm">
            © {new Date().getFullYear()} Sandon Lai. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
}
