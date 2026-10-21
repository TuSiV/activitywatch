<script lang="ts">
import Vue from 'vue';
import LegacyIcon from 'vue-awesome/components/Icon.vue';
import { workspaceIcons } from '~/icons/workspaceIcons';

/** Line icons share a 24px grid; brands and extension-defined glyphs use the legacy renderer. */
export default Vue.extend({
  name: 'WorkspaceIcon',
  inheritAttrs: false,
  props: {
    name: { type: String, default: '' },
    scale: { type: [Number, String], default: 1 },
    title: String,
    label: String,
    spin: Boolean,
    pulse: Boolean,
    inverse: Boolean,
    flip: String,
    tabindex: [Number, String],
  },
  render(h) {
    const nodes = Object.prototype.hasOwnProperty.call(workspaceIcons, this.name)
      ? workspaceIcons[this.name]
      : undefined;
    if (!nodes) {
      return h(
        LegacyIcon,
        {
          props: this.$props,
          attrs: this.$attrs,
          on: this.$listeners,
        },
        this.$slots.default
      );
    }
    const requestedScale = Number(this.scale);
    const size = 16 * (Number.isFinite(requestedScale) && requestedScale > 0 ? requestedScale : 1);
    const accessibleName = this.label || this.title || this.$attrs['aria-label'];
    return h(
      'svg',
      {
        class: {
          'fa-icon': true,
          'aw-line-icon': true,
          'aw-line-icon--spin': this.spin,
          'aw-line-icon--pulse': this.pulse && !this.spin,
          'aw-line-icon--inverse': this.inverse,
          'aw-line-icon--flip-x': this.flip === 'horizontal',
          'aw-line-icon--flip-y': this.flip === 'vertical',
        },
        attrs: {
          ...this.$attrs,
          xmlns: 'http://www.w3.org/2000/svg',
          viewBox: '0 0 24 24',
          width: size,
          height: size,
          fill: 'none',
          stroke: 'currentColor',
          'stroke-width': 1.75,
          'stroke-linecap': 'round',
          'stroke-linejoin': 'round',
          role: accessibleName ? 'img' : undefined,
          'aria-label': accessibleName,
          'aria-hidden': accessibleName ? undefined : 'true',
          focusable: 'false',
          tabindex: this.tabindex,
          'data-icon': this.name,
        },
        on: this.$listeners,
      },
      [
        ...(this.title ? [h('title', this.title)] : []),
        ...nodes.map(([tag, attrs], index) => h(tag, { key: index, attrs })),
      ]
    );
  },
});
</script>
