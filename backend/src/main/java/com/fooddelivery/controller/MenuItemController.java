package com.fooddelivery.controller;

import com.fooddelivery.model.MenuItem;
import com.fooddelivery.service.MenuItemService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/restaurants/{restaurantId}/menu-items")
@CrossOrigin(origins = "http://localhost:8502")
@RequiredArgsConstructor
public class MenuItemController {
    
    private final MenuItemService menuItemService;
    
    @PostMapping
    public ResponseEntity<?> addMenuItem(
            @PathVariable Long restaurantId,
            @RequestBody Map<String, Object> request) {
        try {
            MenuItem menuItem = menuItemService.addMenuItem(
                restaurantId,
                (String) request.get("name"),
                (String) request.get("description"),
                Double.parseDouble(request.get("price").toString())
            );
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Menu item added successfully",
                "menuItem", Map.of(
                    "id", menuItem.getId(),
                    "name", menuItem.getName(),
                    "description", menuItem.getDescription(),
                    "price", menuItem.getPrice(),
                    "isAvailable", menuItem.isAvailable()
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
    public ResponseEntity<?> getMenuItems(@PathVariable Long restaurantId) {
        try {
            List<MenuItem> menuItems = menuItemService.getMenuItemsByRestaurant(restaurantId);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "menuItems", menuItems.stream().map(item -> Map.of(
                    "id", item.getId(),
                    "name", item.getName(),
                    "description", item.getDescription(),
                    "price", item.getPrice(),
                    "isAvailable", item.isAvailable()
                )).toList()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @DeleteMapping("/{menuItemId}")
    public ResponseEntity<?> deleteMenuItem(
            @PathVariable Long restaurantId,
            @PathVariable Long menuItemId) {
        try {
            menuItemService.deleteMenuItem(menuItemId);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Menu item deleted successfully"
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @PutMapping("/{menuItemId}/toggle-availability")
    public ResponseEntity<?> toggleMenuItemAvailability(
            @PathVariable Long restaurantId,
            @PathVariable Long menuItemId) {
        try {
            MenuItem menuItem = menuItemService.toggleMenuItemAvailability(menuItemId);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Menu item availability updated successfully",
                "isAvailable", menuItem.isAvailable()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
} 