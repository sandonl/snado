export default function Footer() {
  return (
    <footer>
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="text-center text-muted-foreground text-sm">
          © {new Date().getFullYear()} Sandon Lai. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
