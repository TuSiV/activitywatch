<template lang="pug">
//- Desktop and mobile share route entries and capability checks.
mixin navMain
  // If only a single view (the default) is available
  b-nav-item(v-if="activityViews && activityViews.length === 1", v-for="view in activityViews", :key="view.name", :to="view.pathUrl")
    div.px-2.px-lg-1
      icon(name="calendar-day")
      | {{ $t('nav.activity') }}

  // If multiple (or no) activity views are available
  b-nav-item-dropdown(v-if="!activityViews || activityViews.length !== 1")
    template(slot="button-content")
      div.d-inline.px-2.px-lg-1
        icon(name="calendar-day")
        | {{ $t('nav.activity') }}
    b-dropdown-item(v-if="activityViews === null", disabled)
      span.text-muted {{ $t('nav.loading') }}
      br
    b-dropdown-item(v-else-if="activityViews && activityViews.length <= 0", disabled)
      | {{ $t('nav.noActivityReports') }}
    b-dropdown-item(v-for="view in activityViews", :key="view.name", :to="view.pathUrl")
      icon(:name="view.icon")
      | {{ view.name }}
    // Combined view of every device (incl. synced and mobile ones)
    template(v-if="activityViews && activityViews.length > 1")
      b-dropdown-divider
      b-dropdown-item(:to="allDevicesPathUrl" data-testid="nav-all-devices")
        icon(name="layer-group")
        | {{ $t('activity.allDevices') }}

  b-nav-item(to="/timeline" style="font-color: #000;")
    div.px-2.px-lg-1
      icon(name="stream")
      | {{ $t('nav.timeline') }}

  b-nav-item(to="/stopwatch")
    div.px-2.px-lg-1
      icon(name="stopwatch")
      | {{ $t('nav.stopwatch') }}

mixin navTools(desktop)
  b-nav-item(to="/search")
    icon(name="search")
    | {{ $t('nav.search') }}
  b-nav-item(to="/category-builder" data-testid="nav-category-builder")
    icon(name="tags")
    | {{ $t('nav.categoryBuilder') }}
  b-nav-item(to="/work-report")
    icon(name="briefcase")
    | {{ $t('nav.workReport') }}
  b-nav-item(to="/billing")
    icon(name="dollar-sign")
    | {{ $t('nav.billableHours') }}
  b-nav-item-dropdown
    template(slot="button-content")
      icon(name="tools")
      | {{ $t('nav.tools') }}
    b-dropdown-item(to="/analysis/activity" v-if="devmode")
      icon(name="robot")
      | {{ $t('nav.aiSummary') }}
    b-dropdown-item(to="/trends" v-if="devmode")
      icon(name="chart-line")
      | {{ $t('nav.trends') }}
    b-dropdown-item(to="/report" v-if="devmode")
      icon(name="chart-pie")
      | {{ $t('nav.report') }}
    b-dropdown-item(to="/alerts" v-if="devmode")
      icon(name="flag-checkered")
      | {{ $t('nav.alerts') }}
    b-dropdown-item(to="/timespiral" v-if="devmode")
      icon(name="history")
      | {{ $t('nav.timespiral') }}
    b-dropdown-item(to="/query")
      icon(name="code")
      | {{ $t('nav.query') }}
    b-dropdown-item(to="/graph" v-if="devmode")
      icon(name="project-diagram")
      | {{ $t('nav.graph') }}

  b-nav-item(to="/buckets")
    div.px-2.px-lg-1
      icon(name="database")
      | {{ $t('nav.rawData') }}
  b-nav-item(to="/settings")
    div.px-2.px-lg-1
      icon(name="cog")
      | {{ $t('nav.settings') }}
  if desktop
    +navNativeDropdown
  else
    +navNative

//- Actions only the Android app can perform. Rendered only after the app's
//- native bridge reports them, so browsers never show entries they can't run.
//- Flat entries in the drawer; one dropdown in the desktop navbar, where three
//- more inline links would run into the absolutely centered brand.
mixin navNativeDropdown
  b-nav-item-dropdown(v-if="nativeMenuActions.length" right data-testid="navbar-native-menu")
    template(slot="button-content")
      div.d-inline.px-2.px-lg-1
        icon(name="mobile")
        | {{ $t('nav.app') }}
    b-dropdown-item(
      v-for="action in nativeMenuActions"
      :key="action.id"
      href="#"
      @click.prevent="runNativeAction(action.id)"
      :data-testid="'navbar-native-' + action.id"
    )
      icon(:name="action.icon")
      | {{ $t(action.label) }}

mixin navNative
  b-nav-item(
    v-for="action in nativeMenuActions"
    :key="action.id"
    href="#"
    @click.prevent="runNativeAction(action.id)"
    :data-testid="'nav-native-' + action.id"
  )
    div.px-2.px-lg-1
      icon(:name="action.icon")
      | {{ $t(action.label) }}


div.aw-navigation
  aside.aw-sidebar.d-none.d-lg-flex(:aria-label="$t('app.name')")
    router-link.aw-brand(to="/")
      img(src="/logo.png" alt="" width="32" height="32")
      span {{ $t('app.name') }}
    b-badge.aw-edition(v-if="researchEdition" variant="info" data-testid="research-edition-badge") {{ $t('app.researchEdition') }}
    nav#nav-collapse.aw-sidebar-nav
      b-nav(vertical)
        +navMain
        +navTools(true)

  b-navbar.aw-mobile-header.d-lg-none(fixed="top" toggleable="lg")
    b-navbar-brand(to="/")
      img(src="/logo.png" alt="" width="28" height="28")
      span.ml-2 {{ $t('app.name') }}
      b-badge.ml-2(v-if="researchEdition" variant="info" data-testid="research-edition-badge") {{ $t('app.researchEdition') }}
    b-navbar-toggle(target="nav-drawer" data-testid="nav-drawer-toggle")
  b-sidebar#nav-drawer.aw-nav-drawer(
    v-model="drawerOpen"
    :title="$t('app.name')"
    backdrop
    lazy
    shadow
    width="min(85vw, 320px)"
    bg-variant="white"
    data-testid="nav-drawer"
  )
    b-navbar-nav.px-3.py-2
      +navMain
      +navTools
</template>

<script lang="ts">
// only import the icons you use to reduce bundle size
import 'vue-awesome/icons/calendar-day';
import 'vue-awesome/icons/briefcase';
import 'vue-awesome/icons/dollar-sign';
import 'vue-awesome/icons/calendar-week';
import 'vue-awesome/icons/stream';
import 'vue-awesome/icons/database';
import 'vue-awesome/icons/search';
import 'vue-awesome/icons/code';
import 'vue-awesome/icons/tags';
import 'vue-awesome/icons/chart-line';
import 'vue-awesome/icons/chart-pie';
import 'vue-awesome/icons/flag-checkered';
import 'vue-awesome/icons/stopwatch';
import 'vue-awesome/icons/robot';
import 'vue-awesome/icons/cog';
import 'vue-awesome/icons/tools';
import 'vue-awesome/icons/history';
import 'vue-awesome/icons/project-diagram';
import 'vue-awesome/icons/ellipsis-h';
import 'vue-awesome/icons/mobile';
import 'vue-awesome/icons/desktop';
import 'vue-awesome/icons/layer-group';
import 'vue-awesome/icons/sync';
import 'vue-awesome/icons/key';
import 'vue-awesome/icons/external-link-alt';

import _ from 'lodash';

import { mapState } from 'pinia';
import { useSettingsStore } from '~/stores/settings';
import { useBucketsStore } from '~/stores/buckets';
import { IBucket } from '~/util/interfaces';
import { ALL_DEVICES, formatHostParam } from '~/util/multidevice';
import { connectNativeBridge, NATIVE_MENU_ACTIONS, NativeBridge } from '~/util/nativeBridge';

export default {
  name: 'Header',
  data() {
    return {
      activityViews: null,
      // Sticky on every platform: tall pages (the timeline, a long activity
      // view) otherwise scroll the navigation out of reach.
      // See https://github.com/ActivityWatch/aw-webui/issues/299
      fixedTopMenu: true,
      researchEdition: typeof AW_RESEARCH_EDITION !== 'undefined' && AW_RESEARCH_EDITION,
      allDevicesPathUrl: `/activity/${ALL_DEVICES}`,
      drawerOpen: false,
      desktopQuery: null,
      nativeBridge: null as NativeBridge | null,
      nativeActions: [] as string[],
    };
  },
  computed: {
    ...mapState(useSettingsStore, ['devmode']),
    nativeMenuActions() {
      return NATIVE_MENU_ACTIONS.filter(a => this.nativeActions.includes(a.id));
    },
  },
  watch: {
    drawerOpen(isOpen: boolean) {
      // Lets Android Back dismiss the drawer before leaving the page.
      this.nativeBridge?.reportMenu(isOpen);
    },
  },
  created() {
    this.nativeBridge = connectNativeBridge({
      onCapabilities: (actions: string[]) => {
        this.nativeActions = actions;
      },
      onCloseMenu: () => {
        this.drawerOpen = false;
      },
    });
  },
  mounted: async function () {
    // The drawer only exists below the lg breakpoint: close it (and its backdrop)
    // when the viewport grows to desktop width.
    if (typeof window !== 'undefined' && window.matchMedia) {
      this.desktopQuery = window.matchMedia('(min-width: 992px)');
      // Safari < 14 and old WebViews only have the legacy addListener API.
      if (typeof this.desktopQuery.addEventListener === 'function') {
        this.desktopQuery.addEventListener('change', this.onDesktopQueryChange);
      } else if (typeof this.desktopQuery.addListener === 'function') {
        this.desktopQuery.addListener(this.onDesktopQueryChange);
      }
    }

    const bucketStore = useBucketsStore();
    await bucketStore.ensureLoaded();
    const buckets: IBucket[] = bucketStore.buckets;
    const types_by_host = {};

    const activityViews = [];

    _.each(buckets, v => {
      types_by_host[v.hostname] = types_by_host[v.hostname] || {};
      types_by_host[v.hostname].afk ||= v.type == 'afkstatus';
      types_by_host[v.hostname].window ||= v.type == 'currentwindow';
      types_by_host[v.hostname].android ||= v.type == 'currentwindow' && v.id.includes('android');
    });

    _.each(types_by_host, (types, hostname) => {
      if (types['android']) {
        activityViews.push({
          name: `${hostname} (Android)`,
          hostname: hostname,
          type: 'android',
          pathUrl: `/activity/${formatHostParam([hostname])}`,
          icon: 'mobile',
        });
      } else if (hostname != 'unknown') {
        activityViews.push({
          name: hostname,
          hostname: hostname,
          type: 'default',
          pathUrl: `/activity/${formatHostParam([hostname])}`,
          icon: 'desktop',
        });
      }
    });

    this.activityViews = activityViews;
  },
  beforeDestroy() {
    this.nativeBridge?.disconnect();
    if (this.desktopQuery) {
      if (typeof this.desktopQuery.removeEventListener === 'function') {
        this.desktopQuery.removeEventListener('change', this.onDesktopQueryChange);
      } else if (typeof this.desktopQuery.removeListener === 'function') {
        this.desktopQuery.removeListener(this.onDesktopQueryChange);
      }
    }
  },
  methods: {
    runNativeAction(id: string) {
      this.drawerOpen = false;
      this.nativeBridge?.runAction(id);
    },
    onDesktopQueryChange(e: MediaQueryListEvent) {
      if (e.matches) {
        this.drawerOpen = false;
      }
    },
  },
};
</script>
