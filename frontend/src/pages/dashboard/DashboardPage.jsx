import { useEffect, useRef } from 'react'
import { Row, Col, Alert } from 'react-bootstrap'
import { useApi } from '../../hooks/useApi'
import { getDashboard } from '../../api/dashboard'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorAlert from '../../components/ErrorAlert'
import RoomStatusCard from './RoomStatusCard'
import BoilerStatusCard from './BoilerStatusCard'

export default function DashboardPage() {
  const { data, loading, error, refetch } = useApi(getDashboard)
  const intervalRef = useRef(null)

  useEffect(() => {
    intervalRef.current = setInterval(refetch, 30000)
    return () => clearInterval(intervalRef.current)
  }, [refetch])

  if (loading && !data) return <LoadingSpinner />
  if (error) return <ErrorAlert message={error} />

  const houses = data?.houses || []

  if (houses.length === 0) {
    return <Alert variant="info">No houses configured. Go to Houses to add one.</Alert>
  }

  return (
    <div>
      <h2 className="mb-4">Dashboard</h2>
      {houses.map((house) => (
        <div key={house.house_id} className="mb-4">
          <h4>{house.house_name}</h4>
          <Row>
            <Col md={4}>
              <BoilerStatusCard
                houseId={house.house_id}
                isOn={house.boiler_is_on}
                lastEventAt={house.last_boiler_event_at}
                onRefresh={refetch}
              />
            </Col>
            <Col md={8}>
              {house.rooms.length === 0 ? (
                <Alert variant="light">No rooms configured yet.</Alert>
              ) : (
                house.rooms.map((room) => (
                  <RoomStatusCard key={room.room_id} room={room} />
                ))
              )}
            </Col>
          </Row>
        </div>
      ))}
    </div>
  )
}
