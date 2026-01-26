/**
 * Generates a table of contents (TOC) with Scroll Spy.
 */
function generateTOC({
  contentSelector = "main",
  tocSelector,
  headingSelector = "h1, h2, h3, h4, h5, h6"
}) {
  // Retrieve content container and wrapper container for the generated ToC
  const content = document.getElementById(contentSelector);
  const toc = document.getElementById(tocSelector);
  if (!content || !toc) return;

  // Retrieve all heading in the content container
  const headings = Array.from(content.querySelectorAll(headingSelector));
  if (!headings.length) return;

  // Create ToC structure
  const rootList = document.createElement("ul");
  rootList.className = "list-none space-y-1";

  const listStack = [rootList];
  const linkMap = new Map();

  let currentLevel = 1;
  headings.forEach((heading, index) => {
    const level = parseInt(heading.tagName.substring(1), 10);

    // Create unique ID's (title + index) for the anchor links
    if (!heading.id) {
      heading.id = heading.textContent.toLowerCase().trim().replace(/[^\w]+/g, "-") + "-" + index;
    }

    // Create subtree of the current section
    while (level > currentLevel) {
      const ul = document.createElement("ul");
      ul.className = "list-none pl-2 space-y-1";

      listStack[listStack.length - 1].lastElementChild?.appendChild(ul);
      listStack.push(ul);

      currentLevel++;
    }

    while (level < currentLevel) {
      listStack.pop();
      currentLevel--;
    }

    // Create current entry
    const li = document.createElement("li");
    const a = document.createElement("a");

    a.href = `#${heading.id}`;
    a.textContent = heading.textContent;
    a.className = `
      block
      text-primary
      no-underline
      aria-[current=location]:font-bold
      aria-[current=location]:text-blue-700
      focus-visible:outline
      focus-visible:outline-2
      focus-visible:outline-blue-600
      focus-visible:outline-offset-2
    `.trim();

    li.appendChild(a);
    listStack[listStack.length - 1].appendChild(li);

    linkMap.set(heading, a);
  });

  // Add ToC to wrapper container
  toc.appendChild(rootList);

  // Scroll-Spy (IntersectionObserver)
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;

        // Reset previous entry
        toc
          .querySelectorAll('a[aria-current="location"]')
          .forEach(link =>
            link.removeAttribute("aria-current")
          );

        // Highlight current entry
        linkMap.get(entry.target)?.setAttribute("aria-current", "location");
      });
    },
    {
      // Apply anchor offset for fixed navbar

    }
  );

  headings.forEach(heading => observer.observe(heading));
}
