import { useState } from 'react'
import { Button, Alert } from 'react-bootstrap'
import { runMigrate } from '../../api/setup'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function StepMigrate({ onNext }) {
  const [running, setRunning] = useState(false)
  const [result, setResult] = useState(null)

  const handleMigrate = async () => {
    setRunning(true)
    setResult(null)
    try {
      const res = await runMigrate()
      setResult(res)
      if (res.success) {
        setTimeout(() => onNext(), 1000)
      }
    } catch (e) {
      setResult({ success: false, message: e.message })
    } finally {
      setRunning(false)
    }
  }

  return (
    <div>
      <h4>Step 2: Run Migrations</h4>
      <p className="text-muted">Create or update the database schema.</p>

      {running && <LoadingSpinner text="Running migrations..." />}

      {result && result.success && (
        <Alert variant="success">{result.message}</Alert>
      )}

      {result && !result.success && (
        <Alert variant="danger">{result.message}</Alert>
      )}

      <Button onClick={handleMigrate} disabled={running}>
        {running ? 'Running...' : 'Run Migrations'}
      </Button>
    </div>
  )
}
