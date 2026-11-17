import { Link } from '@tanstack/react-router';

const Header = () => {
  return (
    <header>
      <div>
        <div className="flex justify-between items-center h-32">
          <nav className="flex space-x-8">
            <Link
              to="/"
              className="text-primary hover:text-primary/80 py-2 rounded-md text-sm font-medium"
            >
              Home
            </Link>
            <Link
              to="/posts"
              className="text-primary hover:text-primary/80 py-2 rounded-md text-sm font-medium"
            >
              Posts
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
