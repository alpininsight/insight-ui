class Carousel {
  static instances = new WeakMap();

  constructor(root) {
    if (Carousel.instances.has(root)) {
      return Carousel.instances.get(root);
    }

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

    // Bind handlers for proper cleanup
    this.boundPrevClick = () => { this.prev(); this.restartAutoplay(); };
    this.boundNextClick = () => { this.next(); this.restartAutoplay(); };
    this.boundTouchStart = (e) => { this.startX = e.touches[0].clientX; };
    this.boundTouchEnd = this.handleTouchEnd.bind(this);
    this.boundWindowResize = () => this.resizeItems();
    this.boundDotClicks = [];

    this.dots = [...this.root.querySelectorAll(".carousel-dot")];
    this.dots.forEach((dot, i) => {
      const handler = () => {
        this.index = i;
        this.update();
        this.restartAutoplay();
      };
      this.boundDotClicks.push({ element: dot, handler });
      dot.addEventListener("click", handler);
    });

    this.init();

    Carousel.instances.set(root, this);
  }

  handleTouchEnd(e) {
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
  }

  init() {
    this.resizeItems();
    if (this.showIndex) this.updateIndexText();
    this.update();

    this.prevBtn.addEventListener("click", this.boundPrevClick);
    this.nextBtn.addEventListener("click", this.boundNextClick);
    this.root.addEventListener("touchstart", this.boundTouchStart);
    this.root.addEventListener("touchend", this.boundTouchEnd);

    if (this.autoplayEnabled) this.startAutoplay();

    window.addEventListener("resize", this.boundWindowResize);
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

  /**
   * Destroys the carousel instance and removes all event listeners.
   * Call this before removing the element from DOM.
   */
  destroy() {
    // Stop autoplay interval
    this.stopAutoplay();

    // Remove button listeners
    this.prevBtn.removeEventListener("click", this.boundPrevClick);
    this.nextBtn.removeEventListener("click", this.boundNextClick);

    // Remove touch listeners
    this.root.removeEventListener("touchstart", this.boundTouchStart);
    this.root.removeEventListener("touchend", this.boundTouchEnd);

    // Remove window resize listener
    window.removeEventListener("resize", this.boundWindowResize);

    // Remove dot click handlers
    this.boundDotClicks.forEach(({ element, handler }) => {
      element.removeEventListener("click", handler);
    });
    this.boundDotClicks = [];

    Carousel.instances.delete(this.root);
    this.root = null;
  }

  // Static method for initializing all carousels
  static initAll() {
    document.querySelectorAll(".carousel").forEach(el => {
      if (!Carousel.instances.has(el)) {
        new Carousel(el);
      }
    });
  }
}

// Global initialization method for backwards compatibility
window.initCarousels = function () {
  Carousel.initAll();
};

window.InsightUI = window.InsightUI || {};
window.InsightUI.Carousel = Carousel;
