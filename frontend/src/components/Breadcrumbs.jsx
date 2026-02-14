import { Breadcrumb } from 'react-bootstrap'
import { Link } from 'react-router-dom'

export default function Breadcrumbs({ items }) {
  return (
    <Breadcrumb>
      {items.map((item, i) => {
        const isLast = i === items.length - 1
        return (
          <Breadcrumb.Item
            key={i}
            linkAs={isLast ? undefined : Link}
            linkProps={isLast ? undefined : { to: item.to }}
            active={isLast}
          >
            {item.label}
          </Breadcrumb.Item>
        )
      })}
    </Breadcrumb>
  )
}
