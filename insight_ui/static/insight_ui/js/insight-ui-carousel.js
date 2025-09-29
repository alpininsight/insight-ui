class Carousel {
  constructor(root) {
    this.root = root;
    this.isRTL =
      this.root.dir === "rtl" ||
      document.documentElement.dir === "rtl" ||
      getComputedStyle(this.root).direction === "rtl";
    this.track = root.querySelector(".carousel-track");
    this.items = [...root.querySelectorAll(".carousel-item")];
    this.prevBtn = root.querySelector(".carousel-prev");
    this.nextBtn = root.querySelector(".carousel-next");
    this.dotsContainer = root.querySelector(".carousel-dots");
    this.indexText = root.querySelector(".carousel-index-text");

    this.autoplayEnabled = root.dataset.autoplay === "true";
    this.showDots = root.dataset.showDots === "true";
    this.showIndex = root.dataset.showIndex === "true";
    this.itemsPerSlide = parseInt(root.dataset.itemsPerSlide || "1");

    this.totalSlides = Math.ceil(this.items.length / this.itemsPerSlide);
    this.index = 0;
    this.autoplayInterval = null;

    this.dots = [...this.root.querySelectorAll(".carousel-dot")];
    this.dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        this.index = i;
        this.update();
        this.restartAutoplay();
      });
    });

    this.init();
  }

  init() {
    this.resizeItems();
    if (this.showIndex) this.updateIndexText();
    this.update();

    this.prevBtn.addEventListener("click", () => {
      this.prev();
      this.restartAutoplay();
    });

    this.nextBtn.addEventListener("click", () => {
      this.next();
      this.restartAutoplay();
    });

    this.root.addEventListener("touchstart", (e) => {
      this.startX = e.touches[0].clientX;
    });

    this.root.addEventListener("touchend", (e) => {
      const endX = e.changedTouches[0].clientX;
      const diff = endX - this.startX;
      if (Math.abs(diff) > 50) {
        if ((diff > 0) !== this.isRTL) {
          this.prev();
        } else {
          this.next();
        }
        this.restartAutoplay();
      }
    });

    if (this.autoplayEnabled) this.startAutoplay();

    window.addEventListener("resize", () => this.resizeItems());
  }

  resizeItems() {
    const containerWidth = this.root.clientWidth;
    this.items.forEach(item => {
      item.style.flex = `0 0 ${100 / this.itemsPerSlide}%`;
    });
  }

  update() {
    const offset = this.index * 100 * (this.isRTL ? 1 : -1);
    this.track.style.transform = `translateX(${offset}%)`;
    if (this.showDots) this.updateDots();
    if (this.showIndex) this.updateIndexText();
  }

  next() {
    this.index = (this.index + 1) % this.totalSlides;
    this.update();
  }

  prev() {
    this.index = (this.index - 1 + this.totalSlides) % this.totalSlides;
    this.update();
  }

  startAutoplay() {
    this.autoplayInterval = setInterval(() => this.next(), 5000);
  }

  stopAutoplay() {
    clearInterval(this.autoplayInterval);
  }

  restartAutoplay() {
    if (!this.autoplayEnabled) return;
    this.stopAutoplay();
    this.startAutoplay();
  }

  updateDots() {
    this.dots.forEach((dot, i) => {
      dot.classList.toggle("bg-insight-primary", i === this.index);
      dot.classList.toggle("bg-transparent", i !== this.index);
    });
  }

  updateIndexText() {
    if (this.indexText) {
      this.indexText.textContent = `Seite ${this.index + 1} / ${this.totalSlides}`;
    }
  }
}

// Global initialization method - Use after adding new carousel
// Sets an init flag so that each carousel is only initialized once,
// even if this method is called several times
window.initCarousels = function () {
  document.querySelectorAll(".carousel").forEach(el => {
    if (!el.dataset.carouselInitialized) {
      new Carousel(el);
      el.dataset.carouselInitialized = "true";
    }
  });
};
