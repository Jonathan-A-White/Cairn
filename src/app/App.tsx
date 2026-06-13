import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./Layout";
import { SettingsScreen } from "./SettingsScreen";
import { InventoryHome } from "../contexts/inventory/features/InventoryHome";
import { PlaceScreen } from "../contexts/inventory/features/PlaceScreen";
import { SearchScreen } from "../contexts/inventory/features/SearchScreen";
import { TripsHome } from "../contexts/trips/features/TripsHome";
import { NewTripScreen } from "../contexts/trips/features/NewTripScreen";
import { TripScreen } from "../contexts/trips/features/TripScreen";
import { PeopleScreen } from "../contexts/trips/features/PeopleScreen";

// import.meta.env.BASE_URL is "/cairn/"; strip the trailing slash for the router.
const basename = import.meta.env.BASE_URL.replace(/\/$/, "");

export function App() {
  return (
    <BrowserRouter basename={basename || undefined}>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<InventoryHome />} />
          <Route path="place/:placeId" element={<PlaceScreen />} />
          <Route path="search" element={<SearchScreen />} />
          <Route path="trips" element={<TripsHome />} />
          <Route path="trips/new" element={<NewTripScreen />} />
          <Route path="trips/:tripId" element={<TripScreen />} />
          <Route path="people" element={<PeopleScreen />} />
          <Route path="settings" element={<SettingsScreen />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
