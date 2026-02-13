import { createContext, useContext, useState, useEffect } from 'react'
import { getSetupStatus } from '../api/setup'

const SetupContext = createContext()

export function SetupProvider({ children }) {
  const [setupComplete, setSetupComplete] = useState(null) // null = loading
  const [checking, setChecking] = useState(true)

  const checkSetup = async () => {
    setChecking(true)
    try {
      const status = await getSetupStatus()
      setSetupComplete(status.setup_complete)
    } catch {
      setSetupComplete(false)
    } finally {
      setChecking(false)
    }
  }

  useEffect(() => {
    checkSetup()
  }, [])

  return (
    <SetupContext.Provider value={{ setupComplete, checking, checkSetup, setSetupComplete }}>
      {children}
    </SetupContext.Provider>
  )
}

export function useSetup() {
  return useContext(SetupContext)
}
