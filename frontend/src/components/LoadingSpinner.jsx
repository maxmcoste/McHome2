import { Spinner } from 'react-bootstrap'

export default function LoadingSpinner({ text = 'Loading...' }) {
  return (
    <div className="d-flex align-items-center justify-content-center py-5">
      <Spinner animation="border" role="status" className="me-2" />
      <span>{text}</span>
    </div>
  )
}
