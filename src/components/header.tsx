import Link from "next/link";

const Header = () => {
  return (
    <header>
      <div>
        <div className="flex justify-between items-center h-32">
          <nav className="flex space-x-8">
            <Link
              href="/"
              className="text-primary hover:text-secondary py-2 rounded-md text-sm font-medium"
            >
              Home
            </Link>
            <Link
              href="/posts"
              className="text-primary hover:text-secondary py-2 rounded-md text-sm font-medium"
            >
              Posts
            </Link>
            {/* <Link
              href="/about"
              className="text-primary hover:text-secondary py-2 rounded-md text-sm font-medium"
            >
              About
            </Link> */}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
