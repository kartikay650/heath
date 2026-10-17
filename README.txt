HEATH WEBSITE

Files
  index.html     the site (fonts, styles and scripts are all inside this one file)
  agents.html, index.md, llms.txt, heath.json   plain-text versions of the site for AI agents and crawlers
  server.py, start.command   local preview server (not needed for hosting)

To preview locally
  Mac: double-click start.command (first time: right-click > Open).
  Or in Terminal, inside this folder:  python3 server.py
  Then go to http://localhost:8000 (it opens by itself). Ctrl+C in the Terminal to stop.
  Waitlist signups made on the local preview are saved to waitlist.csv in this folder.

To host
  Upload index.html (plus agents.html, index.md, llms.txt, heath.json if you want them) to any static host:
  Netlify, Vercel, Cloudflare Pages, GitHub Pages. No build step.
  The waitlist form posts to /api/waitlist. On a static host there is no server behind that,
  so wire the form to your own endpoint (or a form service) before launch.

Fonts are trial/test versions (Klim National 2 and Untitled Sans, Pangram Fraktion Mono).
Buy licences before anything goes public.
