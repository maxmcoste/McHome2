import { Card, Badge } from 'react-bootstrap'

export default function RoomStatusCard({ room }) {
  const tempDisplay = room.temperature_c != null
    ? `${room.temperature_c.toFixed(1)} C`
    : 'No data'

  const desiredDisplay = room.desired_temp_c != null
    ? `${room.desired_temp_c.toFixed(1)} C`
    : 'Not set'

  return (
    <Card className="mb-3">
      <Card.Body>
        <Card.Title>{room.room_name}</Card.Title>
        <div className="d-flex justify-content-between align-items-center">
          <div>
            <div className="fs-3 fw-bold">{tempDisplay}</div>
            <small className="text-muted">Target: {desiredDisplay}</small>
          </div>
          <div className="text-end">
            <div>
              <Badge bg={room.windows_open > 0 ? 'warning' : 'secondary'}>
                Windows: {room.windows_open}/{room.windows_total}
              </Badge>
            </div>
            {room.has_prediction && (
              <Badge bg="info" className="mt-1">Prediction active</Badge>
            )}
          </div>
        </div>
      </Card.Body>
    </Card>
  )
}
