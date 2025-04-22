package com.fooddelivery.controller;

import com.fooddelivery.model.Cart;
import com.fooddelivery.service.CartService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import lombok.extern.slf4j.Slf4j;

import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/cart")
@CrossOrigin(origins = "http://localhost:8502")
@RequiredArgsConstructor
public class CartController {
    
    private final CartService cartService;
    
    @GetMapping("/list/active")
    public ResponseEntity<?> getAllActiveCarts() {
        log.info("Getting all active carts");
        try {
            List<Cart> carts = cartService.getAllActiveCarts();
            log.info("Found {} active carts", carts.size());
            
            // Initialize lazy-loaded relationships
            carts.forEach(cart -> {
                cart.getUser().getUsername(); // Initialize user
                cart.getMenuItem().getName(); // Initialize menu item
                cart.getMenuItem().getRestaurant().getName(); // Initialize restaurant
            });
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "carts", carts.stream().map(cart -> Map.of(
                    "id", cart.getId(),
                    "userId", cart.getUser().getId(),
                    "userName", cart.getUser().getUsername(),
                    "restaurantName", cart.getMenuItem().getRestaurant().getName(),
                    "itemName", cart.getMenuItem().getName(),
                    "quantity", cart.getQuantity(),
                    "price", cart.getMenuItem().getPrice(),
                    "totalPrice", cart.getMenuItem().getPrice() * cart.getQuantity()
                )).toList()
            ));
        } catch (Exception e) {
            log.error("Error getting all active carts: {}", e.getMessage());
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @PostMapping("/add")
    public ResponseEntity<?> addToCart(@RequestBody Map<String, Object> request) {
        log.info("Received add to cart request: {}", request);
        try {
            Cart cart = cartService.addToCart(
                Long.parseLong(request.get("userId").toString()),
                Long.parseLong(request.get("menuItemId").toString()),
                Integer.parseInt(request.get("quantity").toString())
            );
            log.info("Successfully added item to cart: {}", cart);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Item added to cart successfully",
                "cart", Map.of(
                    "id", cart.getId(),
                    "menuItem", Map.of(
                        "id", cart.getMenuItem().getId(),
                        "name", cart.getMenuItem().getName(),
                        "price", cart.getMenuItem().getPrice()
                    ),
                    "quantity", cart.getQuantity()
                )
            ));
        } catch (Exception e) {
            log.error("Error adding item to cart: {}", e.getMessage());
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @GetMapping("/{userId}")
    public ResponseEntity<?> getCartItems(@PathVariable Long userId) {
        log.info("Getting cart items for user ID: {}", userId);
        try {
            List<Cart> cartItems = cartService.getCartItems(userId);
            log.info("Found {} cart items", cartItems.size());
            return ResponseEntity.ok(Map.of(
                "success", true,
                "cartItems", cartItems.stream().map(cart -> Map.of(
                    "id", cart.getId(),
                    "menuItem", Map.of(
                        "id", cart.getMenuItem().getId(),
                        "name", cart.getMenuItem().getName(),
                        "price", cart.getMenuItem().getPrice(),
                        "description", cart.getMenuItem().getDescription()
                    ),
                    "quantity", cart.getQuantity()
                )).toList()
            ));
        } catch (Exception e) {
            log.error("Error getting cart items: {}", e.getMessage());
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @DeleteMapping("/{cartId}")
    public ResponseEntity<?> removeFromCart(@PathVariable Long cartId) {
        log.info("Removing cart item with ID: {}", cartId);
        try {
            cartService.removeFromCart(cartId);
            log.info("Successfully removed cart item");
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Item removed from cart successfully"
            ));
        } catch (Exception e) {
            log.error("Error removing cart item: {}", e.getMessage());
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @PutMapping("/{cartId}/quantity")
    public ResponseEntity<?> updateQuantity(
            @PathVariable Long cartId,
            @RequestBody Map<String, Integer> request) {
        log.info("Updating quantity for cart ID: {} to {}", cartId, request.get("quantity"));
        try {
            cartService.updateQuantity(cartId, request.get("quantity"));
            log.info("Successfully updated quantity");
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Quantity updated successfully"
            ));
        } catch (Exception e) {
            log.error("Error updating quantity: {}", e.getMessage());
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @DeleteMapping("/clear/{userId}")
    public ResponseEntity<?> clearCart(@PathVariable Long userId) {
        log.info("Clearing cart for user ID: {}", userId);
        try {
            cartService.clearCart(userId);
            log.info("Successfully cleared cart");
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Cart cleared successfully"
            ));
        } catch (Exception e) {
            log.error("Error clearing cart: {}", e.getMessage());
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
} 