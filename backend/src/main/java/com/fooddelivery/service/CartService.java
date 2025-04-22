package com.fooddelivery.service;

import com.fooddelivery.model.Cart;
import com.fooddelivery.model.MenuItem;
import com.fooddelivery.model.User;
import com.fooddelivery.repository.CartRepository;
import com.fooddelivery.repository.MenuItemRepository;
import com.fooddelivery.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.extern.slf4j.Slf4j;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class CartService {
    
    private final CartRepository cartRepository;
    private final UserRepository userRepository;
    private final MenuItemRepository menuItemRepository;
    
    @Transactional
    public Cart addToCart(Long userId, Long menuItemId, Integer quantity) {
        log.info("Adding item to cart - User ID: {}, Menu Item ID: {}, Quantity: {}", userId, menuItemId, quantity);
        
        User user = userRepository.findById(userId)
            .orElseThrow(() -> {
                log.error("User not found with ID: {}", userId);
                return new RuntimeException("User not found");
            });
            
        MenuItem menuItem = menuItemRepository.findById(menuItemId)
            .orElseThrow(() -> {
                log.error("Menu item not found with ID: {}", menuItemId);
                return new RuntimeException("Menu item not found");
            });
            
        // Check if item already exists in user's cart
        Cart existingCart = cartRepository.findByUser_IdAndMenuItem_IdAndIsActiveTrue(userId, menuItemId)
            .orElse(null);
            
        if (existingCart != null) {
            log.info("Updating existing cart item - Cart ID: {}", existingCart.getId());
            // Update quantity if item exists
            existingCart.setQuantity(existingCart.getQuantity() + quantity);
            return cartRepository.save(existingCart);
        } else {
            log.info("Creating new cart item");
            // Create new cart item
            Cart cart = new Cart();
            cart.setUser(user);
            cart.setMenuItem(menuItem);
            cart.setQuantity(quantity);
            cart.setActive(true);
            Cart savedCart = cartRepository.save(cart);
            log.info("New cart item created with ID: {}", savedCart.getId());
            return savedCart;
        }
    }
    
    public List<Cart> getCartItems(Long userId) {
        log.info("Getting cart items for user ID: {}", userId);
        List<Cart> items = cartRepository.findByUser_IdAndIsActiveTrue(userId);
        log.info("Found {} cart items", items.size());
        return items;
    }
    
    @Transactional
    public void removeFromCart(Long cartId) {
        log.info("Removing cart item with ID: {}", cartId);
        Cart cart = cartRepository.findById(cartId)
            .orElseThrow(() -> {
                log.error("Cart item not found with ID: {}", cartId);
                return new RuntimeException("Cart item not found");
            });
        cart.setActive(false);
        cartRepository.save(cart);
        log.info("Cart item removed successfully");
    }
    
    @Transactional
    public void updateQuantity(Long cartId, Integer quantity) {
        log.info("Updating quantity for cart item ID: {} to {}", cartId, quantity);
        Cart cart = cartRepository.findById(cartId)
            .orElseThrow(() -> {
                log.error("Cart item not found with ID: {}", cartId);
                return new RuntimeException("Cart item not found");
            });
        cart.setQuantity(quantity);
        cartRepository.save(cart);
        log.info("Quantity updated successfully");
    }
    
    @Transactional
    public void clearCart(Long userId) {
        log.info("Clearing cart for user ID: {}", userId);
        List<Cart> cartItems = cartRepository.findByUser_IdAndIsActiveTrue(userId);
        for (Cart cart : cartItems) {
            cart.setActive(false);
            cartRepository.save(cart);
        }
        log.info("Cart cleared successfully");
    }
    
    public List<Cart> getAllActiveCarts() {
        return cartRepository.findByIsActiveTrue();
    }
} 