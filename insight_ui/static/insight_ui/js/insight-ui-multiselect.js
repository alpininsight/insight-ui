class Multiselect {
    static instances = new WeakMap();

    constructor(container) {
        if (Multiselect.instances.has(container)) {
            return Multiselect.instances.get(container);
        }

        this.container = container;
        this.name = container.dataset.name || "multiselect";
        this.max = parseInt(container.dataset.max) || Infinity;
        this.selectedValues = (container.dataset.selected || "").split(',').map(v => v.trim()).filter(Boolean);
        this.focusedIndex = -1;

        this.combobox = this.container.querySelector('[role="combobox"]');
        this.selected = this.container.querySelector('.selected');
        this.tags = this.container.querySelector('.tags');
        this.search = this.container.querySelector('.search');
        this.options = this.container.querySelector('.options');
        this.optionItems = Array.from(this.container.querySelectorAll('.option'));
        this.info = this.container.querySelector('.info');
        this.ariaStatus = this.container.querySelector(`#${this.name}-aria-status`);
        this.selectAllBtn = this.container.querySelector('.select-all');
        this.deselectAllBtn = this.container.querySelector('.deselect-all');

        this.bindEvents();
        this.renderSelected();

        this.updateInfo();
        this.updateAriaStatus();

        Multiselect.instances.set(container, this);

        debugLog("New multiselect created: ", this.container, this.name);
    }

    bindEvents() {
        this.search.addEventListener('input', () => { this.filterOptions(this.search.value); this.toggleDropdown(true); });
        this.search.addEventListener('focus', () => { this.toggleDropdown(true); });
        this.search.addEventListener('blur', () => { this.search.value = ''; this.filterOptions(''); });
        this.selected.addEventListener('click', () => { this.toggleDropdown(true); this.search.focus(); });

        this.search.addEventListener('keydown', e => {
            const visible = this.optionItems.filter(o => o.style.display !== 'none');
            if (e.key === 'ArrowDown') { e.preventDefault(); if (!visible.length) return; this.focusedIndex = (this.focusedIndex + 1) % visible.length; this.focusOption(visible[this.focusedIndex]); }
            else if (e.key === 'ArrowUp') { e.preventDefault(); if (!visible.length) return; this.focusedIndex = (this.focusedIndex - 1 + visible.length) % visible.length; this.focusOption(visible[this.focusedIndex]); }
            else if (e.key === 'Enter') { e.preventDefault(); if (!visible.length) return; if (this.search.value.trim() === '' && this.focusedIndex === -1) return; const opt = this.focusedIndex >= 0 ? visible[this.focusedIndex] : visible[0]; this.toggleSelect(opt); }
            else if (e.key === 'Escape') { this.toggleDropdown(false); }
            else if (e.key === 'Backspace' && this.search.value === '') { if (this.selectedValues.length > 0) this.deselectValue(this.selectedValues[this.selectedValues.length - 1]); }
            else if (e.key === 'Tab') this.toggleDropdown(false);
        });

        this.optionItems.forEach(opt => opt.addEventListener('click', () => this.toggleSelect(opt)));
        document.addEventListener('click', e => { if (!this.container.contains(e.target)) this.toggleDropdown(false); });

        if (this.selectAllBtn) this.selectAllBtn.addEventListener('click', () => { this.selectAll(); });
        if (this.deselectAllBtn) this.deselectAllBtn.addEventListener('click', () => { this.deselectAll(); });
    }

    toggleDropdown(show) { if (show) { this.options.classList.remove('hidden'); this.combobox.setAttribute('aria-expanded', 'true'); } else { this.options.classList.add('hidden'); this.combobox.setAttribute('aria-expanded', 'false'); this.focusedIndex = -1; } }
    focusOption(opt) { this.optionItems.forEach(o => o.classList.remove('bg-blue-50')); if (!opt) return; opt.classList.add('bg-blue-50'); this.combobox.setAttribute('aria-activedescendant', opt.id); }

    toggleSelect(opt) {
        const value = opt.textContent.trim();
        if (this.selectedValues.includes(value)) this.deselectValue(value);
        else {
            if (this.selectedValues.length >= this.max) { this.selected.classList.add('animate-shake', 'border-red-500'); setTimeout(() => this.selected.classList.remove('animate-shake', 'border-red-500'), 300); return; }
            this.selectedValues.push(value);
            opt.classList.add('bg-blue-100', 'text-blue-700'); opt.setAttribute('aria-selected', 'true'); opt.style.display = 'none';
            this.renderSelected();
        }
        this.search.value = ''; this.filterOptions('');
        this.search.focus();
    }

    deselectValue(value) {
        this.selectedValues = this.selectedValues.filter(v => v !== value);
        this.optionItems.forEach(o => { if (o.textContent.trim() === value) { o.classList.remove('bg-blue-100', 'text-blue-700'); o.setAttribute('aria-selected', 'false'); o.style.display = 'block'; } });
        this.renderSelected();
        this.toggleDropdown(true); this.search.focus();
    }

    renderSelected() {
        this.tags.innerHTML = '';
        this.container.querySelectorAll('input[type=hidden]').forEach(i => i.remove());
        this.selectedValues.forEach(value => {
            const tag = document.createElement('span');
            tag.className = 'bg-blue-100 text-blue-700 text-sm px-2 py-0.5 rounded flex items-center gap-1';
            tag.textContent = value;
            const remove = document.createElement('button');
            remove.innerHTML = '&times;';
            remove.className = 'text-blue-500 hover:text-blue-700 ml-1';
            remove.addEventListener('click', e => { e.stopPropagation(); this.deselectValue(value); });
            tag.appendChild(remove);
            this.tags.appendChild(tag);

            const hidden = document.createElement('input');
            hidden.type = 'hidden'; hidden.name = this.name; hidden.value = value;
            this.container.appendChild(hidden);
        });
        this.updateInfo();
        this.updateAriaStatus();
    }

    filterOptions(term) {
        const lower = term.toLowerCase();
        this.optionItems.forEach(opt => {
            const value = opt.textContent.toLowerCase();
            const hiddenBySelection = this.selectedValues.includes(opt.textContent.trim());
            opt.style.display = (!hiddenBySelection && value.includes(lower)) ? 'block' : 'none';
        });
        this.focusedIndex = -1;
    }

    updateInfo() { this.info.textContent = this.max === Infinity ? '' : `${this.selectedValues.length}/${this.max} ausgewählt`; }
    updateAriaStatus() { this.ariaStatus.textContent = `${this.selectedValues.length} Option${this.selectedValues.length !== 1 ? 'en' : ''} ausgewählt`; }

    selectAll() {
        this.optionItems.forEach(opt => {
            const value = opt.textContent.trim();
            if (!this.selectedValues.includes(value)) {
                this.selectedValues.push(value);
                opt.classList.add('bg-blue-100', 'text-blue-700');
                opt.setAttribute('aria-selected', 'true');
                opt.style.display = 'none';
            }
        });
        this.renderSelected(); this.search.focus();
    }

    deselectAll() {
        this.selectedValues = [];
        this.optionItems.forEach(opt => {
            opt.classList.remove('bg-blue-100', 'text-blue-700');
            opt.setAttribute('aria-selected', 'false'); opt.style.display = 'block';
        });
        this.renderSelected(); this.search.focus();
    }

    // Static method for initializing all multiselect elements
    static initAll() {
        document.querySelectorAll('[data-multiselect]').forEach(c => new Multiselect(c));
    }
}

window.InsightUI = window.InsightUI || {};
window.InsightUI.Multiselect = Multiselect;
