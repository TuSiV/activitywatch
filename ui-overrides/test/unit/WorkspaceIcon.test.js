import { mount } from '@vue/test-utils';
import WorkspaceIcon from '~/components/WorkspaceIcon.vue';
import { workspaceIcons } from '~/icons/workspaceIcons';

const legacy = {
  name: 'LegacyIcon',
  props: ['name', 'label'],
  template: '<span class="legacy-icon" />',
};
const renderIcon = (props, extra = {}) =>
  mount(WorkspaceIcon, {
    propsData: props,
    stubs: { 'fa-icon': legacy },
    ...extra,
  });

describe('Workspace icon compatibility', () => {
  test('all registered application glyphs render as stroked SVGs', () => {
    for (const name of Object.keys(workspaceIcons)) {
      const wrapper = renderIcon({ name });
      expect(wrapper.element.tagName.toLowerCase()).toBe('svg');
      expect(wrapper.attributes('fill')).toBe('none');
      expect(wrapper.attributes('stroke')).toBe('currentColor');
      expect(wrapper.attributes('aria-hidden')).toBe('true');
      expect(wrapper.element.children.length).toBeGreaterThan(0);
      wrapper.destroy();
    }
  });

  test.each(['brands/github', 'extension-defined-icon', 'constructor'])(
    'delegates %s to the compatible legacy renderer',
    name => {
      const wrapper = renderIcon({ name, label: 'Brand or extension' });
      expect(wrapper.find('.legacy-icon').exists()).toBe(true);
      expect(wrapper.findComponent(legacy).props('name')).toBe(name);
    }
  );

  test('keeps labelled glyphs accessible and forwards interaction handlers', async () => {
    const clicked = jest.fn();
    const wrapper = renderIcon(
      { name: 'search', title: 'Search', scale: '1.5' },
      { listeners: { click: clicked } }
    );
    expect(wrapper.attributes('role')).toBe('img');
    expect(wrapper.attributes('aria-label')).toBe('Search');
    expect(wrapper.attributes('aria-hidden')).toBeUndefined();
    expect(wrapper.attributes('width')).toBe('24');
    expect(wrapper.find('title').text()).toBe('Search');
    await wrapper.trigger('click');
    expect(clicked).toHaveBeenCalledTimes(1);
  });

  test('preserves explicit aria labels and loading animation options', () => {
    const wrapper = renderIcon(
      { name: 'spinner', spin: true, scale: -1 },
      { attrs: { 'aria-label': 'Loading' } }
    );
    expect(wrapper.attributes('aria-label')).toBe('Loading');
    expect(wrapper.attributes('width')).toBe('16');
    expect(wrapper.classes()).toContain('aw-line-icon--spin');
  });
});
