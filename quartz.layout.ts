import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import { FileTrieNode } from "./quartz/util/fileTrie"

// Explorer のソート: ABC 順ではなく「更新新しい順」にする。
// 日付の供給元は quartz.config.ts の defaultDateType="modified"
// （frontmatter > git > filesystem の優先順。wiki ページは日付 frontmatter を
// 持たないので実質 git の最終更新時刻）。フォルダは配下ページの最新更新日で
// 代表させ、同点はアルファベット順でタイブレークする。
//
// 注意: この関数は .toString() で直列化され、client 側で new Function により
// グローバルスコープで再評価される（quartz/components/scripts/explorer.inline.ts）。
// そのため inner named 関数を置かない: esbuild の --keep-names が注入する
// __name(...) 参照が再評価時に未定義となり壊れる。named helper を使わず、
// 各ノードの部分木最新日時を反復（明示スタック）で求める。
const sortByRecency = (a: FileTrieNode, b: FileTrieNode): number => {
  const times = [0, 0]
  const roots = [a, b]
  for (let i = 0; i < 2; i++) {
    const stack = [roots[i]]
    while (stack.length > 0) {
      const node = stack.pop() as FileTrieNode
      if (node.data?.date) {
        times[i] = Math.max(times[i], new Date(node.data.date).getTime())
      }
      for (const child of node.children) {
        stack.push(child)
      }
    }
  }
  const diff = times[1] - times[0] // newest first
  if (diff !== 0) return diff
  return a.displayName.localeCompare(b.displayName, undefined, {
    numeric: true,
    sensitivity: "base",
  })
}

export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/nishio/kouchou-ai-developer-wiki"
    }
  })
}

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index"
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList()
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() }
      ]
    }),
    Component.Explorer({ sortFn: sortByRecency })
  ],
  right: [
    Component.Graph({
      localGraph: { removeSlugs: ["index", "log"] },
      globalGraph: { removeSlugs: ["index", "log"] }
    }),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks()
  ]
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true
        },
        { Component: Component.Darkmode() }
      ]
    }),
    Component.Explorer({ sortFn: sortByRecency })
  ],
  right: []
}
