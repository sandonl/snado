import Link from "next/link";

const Header = () => {
  return (
    <header>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-32">
          <nav className="hidden sm:flex space-x-4">
            <Link
              href="/"
              className="text-primary hover:text-secondary px-3 py-2 rounded-md text-sm font-medium"
            >
              Home
            </Link>
            <Link
              href="/posts"
              className="text-primary hover:text-secondary px-3 py-2 rounded-md text-sm font-medium"
            >
              Posts
            </Link>
            <Link
              href="/about"
              className="text-primary hover:text-secondary px-3 py-2 rounded-md text-sm font-medium"
            >
              About
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
