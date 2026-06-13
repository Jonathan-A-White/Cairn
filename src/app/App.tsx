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

/**
 * Derive the router basename from the actual served path so the app works under
 * any project subpath (GitHub Pages serves this repo at /Cairn/) without
 * hardcoding the name or its case. On a project page the first path segment is
 * the repo; matched with the 404.html SPA redirect (pathSegmentsToKeep = 1).
 */
function routerBasename(): string | undefined {
  const firstSegment = window.location.pathname.split("/").filter(Boolean)[0];
  return firstSegment ? `/${firstSegment}` : undefined;
}

export function App() {
  return (
    <BrowserRouter basename={routerBasename()}>
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
