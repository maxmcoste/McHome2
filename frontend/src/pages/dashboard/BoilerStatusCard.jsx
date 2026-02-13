import { Card, Badge, Button } from 'react-bootstrap'
import { useState } from 'react'
import { overrideBoiler } from '../../api/devices'

export default function BoilerStatusCard({ houseId, isOn, lastEventAt, onRefresh }) {
  const [toggling, setToggling] = useState(false)

  const handleToggle = async () => {
    setToggling(true)
    try {
      await overrideBoiler(houseId, isOn ? 'off' : 'on')
      onRefresh()
    } catch {
      // ignore
    } finally {
      setToggling(false)
    }
  }

  return (
    <Card className="mb-3">
      <Card.Body>
        <Card.Title>
          Boiler{' '}
          <Badge bg={isOn ? 'danger' : 'secondary'}>
            {isOn ? 'ON' : 'OFF'}
          </Badge>
        </Card.Title>
        {lastEventAt && (
          <small className="text-muted d-block mb-2">
            Last event: {new Date(lastEventAt).toLocaleString()}
          </small>
        )}
        <Button
          size="sm"
          variant={isOn ? 'outline-secondary' : 'outline-danger'}
          onClick={handleToggle}
          disabled={toggling}
        >
          {toggling ? 'Toggling...' : (isOn ? 'Turn Off' : 'Turn On')}
        </Button>
      </Card.Body>
    </Card>
  )
}
