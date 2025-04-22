package com.fooddelivery.controller;

import com.fooddelivery.model.Restaurant;
import com.fooddelivery.service.RestaurantService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/restaurants")
@CrossOrigin(origins = "http://localhost:8502")
@RequiredArgsConstructor
public class RestaurantController {
    
    private final RestaurantService restaurantService;
    
    @PostMapping
    public ResponseEntity<?> addRestaurant(@RequestBody Map<String, String> request) {
        try {
            Restaurant restaurant = restaurantService.addRestaurant(
                request.get("name"),
                request.get("address"),
                request.get("phoneNumber")
            );
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Restaurant added successfully",
                "restaurant", Map.of(
                    "id", restaurant.getId(),
                    "name", restaurant.getName(),
                    "address", restaurant.getAddress(),
                    "phoneNumber", restaurant.getPhoneNumber()
                )
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @GetMapping
    public ResponseEntity<?> getAllRestaurants() {
        try {
            List<Restaurant> restaurants = restaurantService.getAllActiveRestaurants();
            return ResponseEntity.ok(Map.of(
                "success", true,
                "restaurants", restaurants.stream().map(restaurant -> Map.of(
                    "id", restaurant.getId(),
                    "name", restaurant.getName(),
                    "address", restaurant.getAddress(),
                    "phoneNumber", restaurant.getPhoneNumber()
                )).toList()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteRestaurant(@PathVariable Long id) {
        try {
            restaurantService.deleteRestaurant(id);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Restaurant deleted successfully"
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
} 