import Home_page from './screens/home_page';
import {Route, createBrowserRouter, createRoutesFromElements, RouterProvider} from 'react-router-dom';
import N_gram_page from './screens/n_gram_page';
import Naive_bays from './screens/naive_bays';
import Log_reg from './screens/log-reg';



const router = createBrowserRouter(
  createRoutesFromElements(  

    <Route path='/'>
      <Route index element={<Home_page/>}/>
      <Route path='/n-gram' element={<N_gram_page/>}/>
      <Route path='/naive-bays' element={<Naive_bays/>}/>
      <Route path='/log-reg' element={<Log_reg/>}/>
    </Route>
  
)
)

function App() {

  return <RouterProvider router={router}/>
}

export default App
