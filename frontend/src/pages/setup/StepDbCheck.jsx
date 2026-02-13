import { useState } from 'react'
import { Button, Alert } from 'react-bootstrap'
import { checkDb } from '../../api/setup'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function StepDbCheck({ onNext }) {
  const [checking, setChecking] = useState(false)
  const [result, setResult] = useState(null)

  const handleCheck = async () => {
    setChecking(true)
    setResult(null)
    try {
      const res = await checkDb()
      setResult(res)
      if (res.connected) {
        setTimeout(() => onNext(), 1000)
      }
    } catch (e) {
      setResult({ connected: false, error: e.message })
    } finally {
      setChecking(false)
    }
  }

  return (
    <div>
      <h4>Step 1: Database Connection</h4>
      <p className="text-muted">Check that the database is reachable.</p>

      {checking && <LoadingSpinner text="Checking database connection..." />}

      {result && result.connected && (
        <Alert variant="success">Database connected successfully!</Alert>
      )}

      {result && !result.connected && (
        <Alert variant="danger">
          Connection failed: {result.error || 'Unknown error'}
        </Alert>
      )}

      <Button onClick={handleCheck} disabled={checking}>
        {checking ? 'Checking...' : 'Check Connection'}
      </Button>
    </div>
  )
}
