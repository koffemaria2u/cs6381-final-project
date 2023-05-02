# Benchmark Results

## Initial Setup

1 traefik proxy pod (hp-mini)
5 whoami pods (2x hp-mini, 3x rpi)

### Concurrent Single-Thread

1000 messages
8.857s
112.91 m/s

1000 messages
7.782s
128.50 m/s

1000 messages
7.194s
139.00 m/s

### Concurrent Multi-Thread (6)

6000 messages
13.221s
453.82 m/s

6000 messages
13.853s
433.12 m/s


6000 messages
13.437s
446.53 m/s

### Concurrent Multi-Thread (12)

12000 messages
35.177s
341.13 m/s

12000 messages
32.022s
374.74 m/s

12000 messages
34.746s
345.36 m/s


## Removing RPi

1 traefik proxy pod (hp-mini)
5 whoami pods (hp-mini)

### Concurrent Multi-Thread (12)

12000 messages
24.353s
492.75 m/s

12000 messages
45.140s
 m/s

12000 messages
66.973s
 m/s

## Scaling Traefik

## Removing RPi

3 traefik proxy pod (1x hp-mini, 2x rpi)
5 whoami pods (hp-mini)

### Concurrent Multi-Thread (12)

12,000 messages
26,342s

12,000 messages
34.832s

12,000 messages
34.695s
