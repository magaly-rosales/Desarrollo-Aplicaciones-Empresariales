// Shared rule: how many cards fit per row for a given width
export function getColumns(width) {
  if (width < 500) return 1
  if (width < 768) return 2
  if (width < 1024) return 3
  return 4
}