import { Link } from '@tanstack/react-router';

const Header = ({ isHome }: { isHome: boolean }) => {
  if (isHome) return <header className="portfolio-home-header">
    <Link to="/" className="portfolio-wordmark" aria-label="Sandon Lai, home">sandon lai</Link>
    <nav aria-label="Main navigation"><Link to="/" activeProps={{ 'aria-current': 'page' }}>Home</Link><Link to="/posts">Posts</Link><Link to="/world">Explore</Link></nav>
  </header>
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
            <Link
              to="/world"
              className="text-primary hover:text-primary/80 py-2 rounded-md text-sm font-medium"
            >
              Explore
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
