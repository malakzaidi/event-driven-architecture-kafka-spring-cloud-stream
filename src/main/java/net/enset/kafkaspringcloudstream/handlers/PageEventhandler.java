package net.enset.kafkaspringcloudstream.handlers;


import net.enset.kafkaspringcloudstream.events.PageEvent;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.Random;
import java.util.function.Consumer;
import java.util.function.Supplier;

@Component
public class PageEventhandler {
    @Bean
    public Consumer<PageEvent> pageEventConsumer(){
        return (input) ->{
            System.out.println("*******************");
            System.out.println(input.toString());
            System.out.println("*******************");
        };
    }
    @Bean
    public Supplier<PageEvent> pageEventSupplier(){
        return ()-> {
            return new PageEvent(
                     Math.random()>0.5?"p1":"p2",
                     Math.random()>0.5?"U1":"U2",
                     new Date(),
                     10+new Random().nextInt(10000)
            );
        };
    }
}
