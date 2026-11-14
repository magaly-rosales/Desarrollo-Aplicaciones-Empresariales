import Skeleton, { SkeletonTheme } from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import './SkeletonCard.css'

// Placeholder shown while premieres are loading
function SkeletonCard() {
  return (
    <SkeletonTheme baseColor="#1a1a24" highlightColor="#2f2f40">
      <div className="skeleton-card">
        <Skeleton height={260} borderRadius={12} />
        <Skeleton height={22} width="80%" />
        <Skeleton height={14} width="50%" />
      </div>
    </SkeletonTheme>
  )
}

export default SkeletonCard