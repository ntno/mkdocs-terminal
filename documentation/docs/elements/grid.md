<style>
    .image-grid {
      display: grid;
      grid-template-rows: auto;
      display: grid;
      grid-gap: 1em;
      grid-template-rows: auto;
      grid-template-columns: repeat(
        auto-fit,
        minmax(calc(var(--page-width) / 12), 1fr)
      );
    }
</style>

<section>
<header>
	<h2 id="GridSystem">Grid System</h2>
	<p>
	Terminal CSS has no build-in grid system. However, you can roll your own with Flexbox or CSS Grid.
	</p>
</header>
<div class="image-grid">
  <a href="https://picsum.photos" style="border: none;"
    ><img
      src="https://picsum.photos/200/300?random&1"
      width="auto"
      height="auto"
      alt="random image"
  /></a>
  <a href="https://picsum.photos" style="border: none;"
    ><img
      src="https://picsum.photos/200/300?random&2"
      width="auto"
      height="auto"
      alt="random image"
  /></a>
  <a href="https://picsum.photos" style="border: none;"
    ><img
      src="https://picsum.photos/200/300?random&3"
      width="auto"
      height="auto"
      alt="random image"
  /></a>
  <a href="https://picsum.photos" style="border: none;"
    ><img
      src="https://picsum.photos/200/300?random&4"
      width="auto"
      height="auto"
      alt="random image"
  /></a>
  <a href="https://picsum.photos" style="border: none;"
    ><img
      src="https://picsum.photos/200/300?random&5"
      width="auto"
      height="auto"
      alt="random image"
  /></a>
  <a href="https://picsum.photos" style="border: none;"
    ><img
      src="https://picsum.photos/200/300?random&6"
      width="auto"
      height="auto"
      alt="random image"
  /></a>
  <a href="https://picsum.photos" style="border: none;"
    ><img
      src="https://picsum.photos/200/300?random&7"
      width="auto"
      height="auto"
      alt="random image"
  /></a>
</div>
</section>