import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from './hooks/useAppStore';
import { loadUser } from './store/authSlice';
import AppRouter from './routes/AppRouter';

export default function App() {
  const dispatch = useAppDispatch();
  const { token } = useAppSelector((s) => s.auth);

  useEffect(() => {
    if (token) {
      dispatch(loadUser());
    }
  }, [token, dispatch]);

  return <AppRouter />;
}
