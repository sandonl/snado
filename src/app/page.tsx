import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-48 border-b pb-8">
      <div className="flex flex-col gap-6">
        <h1 className="text-3xl font-bold">About</h1>
        <p className="text-sm">Hi,</p>
        <p className="text-sm">
          I&apos;m a software engineer living in Melbourne, Australia and
          currently work at{" "}
          <Link
            href="https://tilt.legal"
            className="text-zinc-400 hover:text-zinc-500"
          >
            TILT Legal
          </Link>
          . Currently I&apos;m working on making tools and products for legal
          professionals.
        </p>
        <p className="text-sm">
          I graduated from the University of Melbourne with a Bachelor of
          Commerce and Masters of Information Technology at the end of 2022.
        </p>
        <p className="text-sm">
          To find out more about my professional journey and interests, feel
          free to explore my{" "}
          <Link href="/posts" className="text-zinc-400 hover:text-zinc-500">
            written works
          </Link>{" "}
          and various social media profiles.
        </p>
      </div>
    </div>
  );
}
