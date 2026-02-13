import { Button } from 'react-bootstrap'
import { Alert } from 'react-bootstrap'

export default function StepComplete({ onFinish }) {
  return (
    <div>
      <h4>Setup Complete</h4>
      <Alert variant="success">
        Your McHome2 system is configured and ready to use!
      </Alert>
      <p>You can now add rooms, devices, and schedules from the dashboard.</p>
      <Button onClick={onFinish}>Go to Dashboard</Button>
    </div>
  )
}
